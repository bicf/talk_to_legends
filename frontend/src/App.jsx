import { useState, useEffect, useRef } from 'react'
import Box from '@mui/material/Box'
import Drawer from '@mui/material/Drawer'
import Typography from '@mui/material/Typography'
import Autocomplete from '@mui/material/Autocomplete'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import InputAdornment from '@mui/material/InputAdornment'
import Paper from '@mui/material/Paper'
import Link from '@mui/material/Link'
import Divider from '@mui/material/Divider'
import SendIcon from '@mui/icons-material/Send'
import AddIcon from '@mui/icons-material/Add'
import RemoveIcon from '@mui/icons-material/Remove'
import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const DRAWER_WIDTH = 300


export default function App() {
  const [legends, setLegends] = useState([])
  const [legend, setLegend] = useState(null)
  const [lang, setLang] = useState('en')
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [llmUrl, setLlmUrl] = useState('')
  const [llmModel, setLlmModel] = useState('')
  const [availableModels, setAvailableModels] = useState([])
  const [modelsLoading, setModelsLoading] = useState(false)
  const [llmApiKey, setLlmApiKey] = useState('')
  const [showApiKey, setShowApiKey] = useState(false)
  const [fontSize, setFontSize] = useState(14)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (llmUrl && (llmUrl.includes('api.regolo.ai') || llmUrl.includes('openrouter.ai'))) {
      setModelsLoading(true)
      fetch(`${llmUrl}/models`, {
        headers: llmApiKey ? { 'Authorization': `Bearer ${llmApiKey}` } : {}
      })
        .then((res) => res.json())
        .then((data) => {
          if (data && data.data && Array.isArray(data.data)) {
            setAvailableModels(data.data.map(m => m.id))
          } else {
            setAvailableModels([])
          }
        })
        .catch((err) => {
          console.error('Failed to fetch models:', err)
          setAvailableModels([])
        })
        .finally(() => setModelsLoading(false))
    } else {
      setAvailableModels([])
    }
  }, [llmUrl, llmApiKey])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    fetch('/api/setting/legends')
      .then((res) => res.json())
      .then((data) => {
        setLegends(data)
        const params = new URLSearchParams(window.location.search)
        const sid = params.get('session_id')
        if (sid) {
          fetch(`/api/chat/session/${sid}`)
            .then((res) => {
              if (!res.ok) throw new Error('Session not found')
              return res.json()
            })
            .then((dataSession) => {
              setSessionId(dataSession.id)
              setMessages(dataSession.messages || [])
              setLang(dataSession.lang)
              const foundLegend = data.find(leg => leg.id === dataSession.legend_id)
              if (foundLegend) {
                setLegend(foundLegend)
              }
            })
            .catch((err) => {
              console.error('Failed to load session from URL:', err)
              const url = new URL(window.location)
              url.searchParams.delete('session_id')
              window.history.pushState({}, '', url)
            })
        }
      })
      .catch((err) => console.error('Failed to fetch legends:', err))
  }, [])

  const handleSend = () => {
    const text = input.trim()
    if (!text || !sessionId || !llmUrl || !llmModel || !llmApiKey) return
    
    const userMsg = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    fetch(`/api/chat/session/${sessionId}/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        content: text,
        llm_url: llmUrl || undefined,
        llm_model: llmModel || undefined,
        llm_api_key: llmApiKey || undefined
      })
    })
      .then((res) => res.json())
      .then((data) => {
        setLoading(false)
        if (data.assistant) {
          setMessages((prev) => [...prev, data.assistant])
        }
      })
      .catch((err) => {
        setLoading(false)
        console.error('Failed to send message:', err)
      })
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const startSession = (v, l) => {
    setSessionId(null)
    setMessages([])
    if (v && l) {
      fetch('/api/chat/session/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ legend_id: v.id, lang: l })
      })
        .then((res) => res.json())
        .then((data) => {
          setSessionId(data.id)
          setMessages(data.messages || [])
          // Update URL with session_id
          const url = new URL(window.location)
          url.searchParams.set('session_id', data.id)
          window.history.pushState({}, '', url)
        })
        .catch((err) => console.error('Failed to start session:', err))
    } else {
      // Clear session_id from URL if no legend selected
      const url = new URL(window.location)
      url.searchParams.delete('session_id')
      window.history.pushState({}, '', url)
    }
  }


  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
            p: 2,
          },
        }}
      >
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
          Chat with legends
        </Typography>
        <Autocomplete
          options={legends}
          getOptionLabel={(option) => option.name || ''}
          isOptionEqualToValue={(option, value) => option.id === value?.id}
          value={legend}
          onChange={(_, v) => {
            setLegend(v)
            startSession(v, lang)
          }}
          autoHighlight
          renderInput={(params) => (
            <TextField {...params} label="Choose a legend" size="small" sx={{ mb: 2 }} />
          )}
        />
        <TextField
          select
          label="Select language"
          value={lang}
          onChange={(e) => {
            setLang(e.target.value)
            startSession(legend, e.target.value)
          }}
          SelectProps={{ native: true }}
          fullWidth
          size="small"
        >
          <option value="en">English</option>
          <option value="it">Italiano</option>
          <option value="fr">Français</option>
          <option value="de">Deutsch</option>
        </TextField>

        <Divider sx={{ my: 2 }} />

        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
          LLM Settings (Override)
        </Typography>
        <TextField
          label="LLM URL"
          placeholder="http://localhost:11434/v1"
          size="small"
          fullWidth
          required
          error={!llmUrl}
          helperText={!llmUrl ? "LLM URL is required" : ""}
          value={llmUrl}
          onChange={(e) => setLlmUrl(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Autocomplete
          freeSolo
          options={availableModels}
          loading={modelsLoading}
          value={llmModel}
          onInputChange={(_, newValue) => setLlmModel(newValue)}
          renderInput={(params) => (
            <TextField
              {...params}
              label="LLM Model"
              placeholder="gemma2:2b"
              size="small"
              fullWidth
              required
              error={!llmModel}
              helperText={!llmModel ? "LLM Model is required" : ""}
              sx={{ mb: 2 }}
            />
          )}
        />
        <TextField
          label="LLM API Key"
          type={showApiKey ? 'text' : 'password'}
          size="small"
          fullWidth
          required
          error={!llmApiKey}
          helperText={!llmApiKey ? "LLM API Key is required" : ""}
          value={llmApiKey}
          onChange={(e) => setLlmApiKey(e.target.value)}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={() => setShowApiKey(!showApiKey)}
                  onMouseDown={(e) => e.preventDefault()}
                  edge="end"
                  size="small"
                >
                  {showApiKey ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        <Typography variant="caption" sx={{ mt: 1, display: 'block', color: 'text.secondary' }}>
          Get an API key from{' '}
          <Link href="https://regolo.ai" target="_blank" rel="noopener">
            Regolo
          </Link>{' '}
          or{' '}
          <Link href="https://openrouter.ai" target="_blank" rel="noopener">
            OpenRouter
          </Link>.
        </Typography>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          bgcolor: 'grey.50',
        }}
      >
        <Box sx={{ px: 3, py: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">
            {legend ? `Chatting with ${legend.name}` : 'Select a legend to start'}
          </Typography>
          <Box>
            <IconButton size="small" onClick={() => setFontSize(prev => Math.max(prev - 2, 8))}>
              <RemoveIcon fontSize="small" />
            </IconButton>
            <IconButton size="small" onClick={() => setFontSize(prev => Math.min(prev + 2, 32))}>
              <AddIcon fontSize="small" />
            </IconButton>
          </Box>
        </Box>
        <Divider />

        <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 3 }}>
          {messages.length === 0 ? (
            <Typography color="text.secondary">No messages yet.</Typography>
          ) : (
            <>
              {messages.map((m, i) => (
                <Box
                  key={i}
                  sx={{
                    display: 'flex',
                    justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start',
                    mb: 1,
                  }}
                >
                  <Paper
                    sx={{
                      p: 1.5,
                      maxWidth: '70%',
                      bgcolor: m.role === 'user' ? 'primary.main' : 'background.paper',
                      color: m.role === 'user' ? 'primary.contrastText' : 'text.primary',
                      fontSize: `${fontSize}px`,
                      '& p': { m: 0, fontSize: 'inherit' },
                      '& pre': { whiteSpace: 'pre-wrap', wordBreak: 'break-all', fontSize: 'inherit' },
                      '& table': { borderCollapse: 'collapse', my: 1, width: '100%', fontSize: 'inherit' },
                      '& th, & td': { border: '1px solid', borderColor: 'divider', p: 1, fontSize: 'inherit' },
                      '& th': { bgcolor: 'action.hover' },
                    }}
                    elevation={1}
                  >
                    <Typography variant="body2" component="div" sx={{ fontSize: 'inherit' }}>
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                    </Typography>
                  </Paper>
                </Box>
              ))}
              {loading && (
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'flex-start',
                    mb: 1,
                  }}
                >
                  <Paper
                    sx={{
                      p: 1.5,
                      maxWidth: '70%',
                      bgcolor: 'background.paper',
                      color: 'text.primary',
                    }}
                    elevation={1}
                  >
                    <Typography variant="body2" component="div">
                      <Box
                        sx={{
                          display: 'inline-flex',
                          '& span': {
                            display: 'inline-block',
                            width: '0.3rem',
                            height: '0.3rem',
                            borderRadius: '50%',
                            backgroundColor: 'text.secondary',
                            margin: '0 0.1rem',
                            animation: 'bounce 1.4s infinite ease-in-out both',
                          },
                          '& span:nth-of-type(1)': {
                            animationDelay: '-0.32s',
                          },
                          '& span:nth-of-type(2)': {
                            animationDelay: '-0.16s',
                          },
                          '@keyframes bounce': {
                            '0%, 80%, 100%': {
                              transform: 'scale(0)',
                            },
                            '40%': {
                              transform: 'scale(1)',
                            },
                          },
                        }}
                      >
                        <span />
                        <span />
                        <span />
                      </Box>
                    </Typography>
                  </Paper>
                </Box>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </Box>

        <Divider />
        <Box sx={{ p: 2, display: 'flex', gap: 1, alignItems: 'center', bgcolor: 'background.paper' }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            multiline
            maxRows={4}
            sx={{
              '& .MuiInputBase-input': { fontSize: `${fontSize}px` },
            }}
          />
          <IconButton color="primary" onClick={handleSend} disabled={!input.trim() || !llmUrl || !llmModel || !llmApiKey}>
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  )
}