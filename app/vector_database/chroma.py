import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import hashlib
import os
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection_name = "transaction_history"

#check if dir exists
if not os.path.exists("db/latent"):
    os.makedirs("db/latent")
# get path to db
path = os.path.abspath("db/latent")
client = chromadb.PersistentClient(path=path)

collection = client.get_or_create_collection(name=collection_name)


def generate_id(id, booking_date, amount, description):
    unique_string = f"{id}{booking_date}{amount}{description}"
    hash_object = hashlib.sha256(unique_string.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex

def embed(text):
    return default_ef(text)


def load_dataframe(df):
    df['embedding'] = df.apply(lambda row: embed(row['enhanced_description'] + ' '.join(row['categories'])), axis=1)
    #make id from hashing account_id+booking_date+amount+description
    df['id'] = df.apply(lambda row: generate_id(row['account_id'], row['booking_date'], row['amount'], row['description']), axis=1)
    metadatas = df[
        ['booking_date', 'value_date', 'enhanced_description', 'categories', 'amount', 'account_id']].to_dict(
        orient='records')
    print(metadatas)
    """
    collection.add(
        ids=df['id'].tolist(),
        embeddings=df['embedding'].tolist(),
        metadatas= df[['booking_date', 'value_date', 'enhanced_description', 'categories', 'amount', 'account_id']].to_dict(orient='records')
    )
    print(collection.count())
    """

