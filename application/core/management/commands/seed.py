import random
from django.core.management.base import BaseCommand
from django.db import transaction

from application.user.models import CustomUser
from application.profiles.models import Follow
from application.artworks.models import Artwork, Collection, Category, ArtworkImage

from faker import Faker


class Command(BaseCommand):
    help = "Seeds the database with realistic test data."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        CustomUser.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Creating new data...")

        fake = Faker()

        categories = []
        category_names = ["Oil Painting", "Sculpture", "Abstract", "Photography", "Digital Art", "Handcraft"]
        for name in category_names:
            category = Category.objects.create(name=name)
            categories.append(category)
        self.stdout.write(f"Created {len(categories)} categories.")

        profiles = []
        for i in range(10):
            username = f'artist_{i + 1}'
            email = f'{username}@example.com'
            password = 'passwordroottest'

            user = CustomUser.objects.create_user(email=email, username=username, password=password)

            profile = user.profile
            profile.display_name = fake.name()
            profile.bio = fake.paragraph(nb_sentences=3)
            profile.save()
            profiles.append(profile)
        self.stdout.write(f"Created {len(profiles)} users and profiles.")

        for profile in profiles:
            num_follows = random.randint(2, 5)
            followed_profiles = random.sample([p for p in profiles if p != profile], num_follows)
            for followed in followed_profiles:
                Follow.objects.create(follower=profile, following=followed)
        self.stdout.write("Created follow relationships.")

        for profile in profiles:
            for _ in range(random.randint(1, 3)):
                collection = Collection.objects.create(
                    author=profile,
                    title=fake.catch_phrase(),
                    description=fake.sentence()
                )

                for _ in range(random.randint(3, 7)):
                    artwork = Artwork.objects.create(
                        author=profile,
                        title=fake.sentence(nb_words=4),
                        description=fake.paragraph(nb_sentences=5),
                        price=random.randint(50, 2000),
                    )
                    artwork.categories.set(random.sample(categories, random.randint(1, 3)))

                    collection.artworks.add(artwork)

                    for j in range(random.randint(1, 4)):
                        is_cover = (j == 0)
                        ArtworkImage.objects.create(artwork=artwork, is_cover=is_cover)

        self.stdout.write("Created artworks, images, and collections.")
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))