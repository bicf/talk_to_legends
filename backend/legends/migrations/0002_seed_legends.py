from django.db import migrations
from django.utils.text import slugify


LEGENDS = [
    ("Albert Einstein", "Theoretical physicist, 1879–1955, general relativity."),
    ("Leonardo da Vinci", "Renaissance polymath, 1452–1519."),
    ("Marie Curie", "Physicist and chemist, 1867–1934, radioactivity."),
    ("Nikola Tesla", "Inventor and electrical engineer, 1856–1943."),
    ("Isaac Newton", "Mathematician and physicist, 1643–1727."),
    ("Ada Lovelace", "Mathematician, 1815–1852, first computer programmer."),
    ("Cleopatra", "Last active pharaoh of Ptolemaic Egypt, 69–30 BC."),
    ("Napoleon Bonaparte", "French military and political leader, 1769–1821."),
    ("William Shakespeare", "English playwright and poet, 1564–1616."),
    ("Mahatma Gandhi", "Indian independence leader, 1869–1948."),
    ("Martin Luther King Jr.", "American civil rights leader, 1929–1968."),
    ("Abraham Lincoln", "16th US President, 1809–1865."),
    ("Socrates", "Classical Greek philosopher, 470–399 BC."),
    ("Plato", "Classical Greek philosopher, 428–348 BC."),
    ("Aristotle", "Classical Greek philosopher, 384–322 BC."),
]


def seed(apps, schema_editor):
    Legend = apps.get_model("legends", "Legend")
    for name, description in LEGENDS:
        Legend.objects.update_or_create(
            slug=slugify(name),
            defaults={"name": name, "description": description},
        )


def unseed(apps, schema_editor):
    Legend = apps.get_model("legends", "Legend")
    Legend.objects.filter(slug__in=[slugify(n) for n, _ in LEGENDS]).delete()


class Migration(migrations.Migration):
    dependencies = [("legends", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]