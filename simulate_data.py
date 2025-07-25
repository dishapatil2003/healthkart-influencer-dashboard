import pandas as pd
import random
from faker import Faker

fake = Faker()

# ----- Simulate influencers -----
influencers = []
platforms = ['Instagram', 'YouTube', 'Twitter']
categories = ['Fitness', 'Health', 'Lifestyle', 'Nutrition']
genders = ['Male', 'Female']

for i in range(30):
    influencers.append({
        'ID': i + 1,
        'name': fake.name(),
        'category': random.choice(categories),
        'gender': random.choice(genders),
        'follower_count': random.randint(10000, 1000000),
        'platform': random.choice(platforms)
    })

df_influencers = pd.DataFrame(influencers)
df_influencers.to_csv('influencers.csv', index=False)

# ----- Simulate posts -----
posts = []
for i in range(100):
    inf_id = random.choice(df_influencers['ID'])
    platform = random.choice(platforms)
    posts.append({
        'influencer_id': inf_id,
        'platform': platform,
        'date': fake.date_this_year(),
        'URL': fake.url(),
        'caption': fake.sentence(),
        'reach': random.randint(1000, 100000),
        'likes': random.randint(50, 10000),
        'comments': random.randint(5, 1000),
    })

df_posts = pd.DataFrame(posts)
df_posts.to_csv('posts.csv', index=False)

# ----- Simulate tracking_data -----
tracking = []
products = ['Whey Protein', 'Omega-3', 'Multivitamin', 'Pre-Workout']
sources = ['Instagram', 'YouTube', 'Twitter']
campaigns = ['Summer2025', 'FitLife', 'BoostUp']

for i in range(500):
    tracking.append({
        'source': random.choice(sources),
        'campaign': random.choice(campaigns),
        'influencer_id': random.choice(df_influencers['ID']),
        'user_id': fake.uuid4(),
        'product': random.choice(products),
        'date': fake.date_this_year(),
        'orders': random.randint(1, 5),
        'revenue': round(random.uniform(100, 1000), 2)
    })

df_tracking = pd.DataFrame(tracking)
df_tracking.to_csv('tracking_data.csv', index=False)

# ----- Simulate payouts -----
payouts = []
for inf in df_influencers['ID']:
    basis = random.choice(['post', 'order'])
    rate = random.randint(500, 5000)
    orders = random.randint(1, 50)
    payout = rate * (orders if basis == 'order' else 1)
    payouts.append({
        'influencer_id': inf,
        'basis': basis,
        'rate': rate,
        'orders': orders,
        'total_payout': payout
    })

df_payouts = pd.DataFrame(payouts)
df_payouts.to_csv('payouts.csv', index=False)

print("✅ Data simulation completed and saved to CSV files.")
