import pandas as pd
from sklearn.cluster import KMeans
import psycopg2
from config.config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST

def train_model():
    try:
        conn = psycopg2.connect(
            dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST
        )
        df = pd.read_sql("SELECT * FROM clean_data", conn)
        conn.close()

        if df.empty:
            print("⚠️ No data found in clean_data.")
            return

        print("✅ Data loaded. Columns:", df.columns.tolist())

        # Unsupervised clustering just on lat/lon
        coords = df[['latitude', 'longitude']].dropna()
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(coords)

        print("✅ Clustering complete. Labels:")
        print(kmeans.labels_[:10])

    except Exception as e:
        print(f"❌ Model training error: {e}")

if __name__ == '__main__':
    train_model()
