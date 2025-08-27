import { MongoClient, Db } from "mongodb";
import dotenv from "dotenv";
import { User , RquestHistory } from "./models/schema";

dotenv.config();

const uri = process.env.MONGODB_URI!;
const dbName = process.env.MONGODB_DB!;

let client: MongoClient;
let db: Db;

export async function connectDB(): Promise<Db> {
  if (db) return db;

  client = new MongoClient(uri);
  await client.connect();
  db = client.db(dbName);

  console.log(`✅ Connected to MongoDB: ${dbName}`);
  return db;
}

export async function disconnectDB(): Promise<void> {
  if (client) {
    await client.close();
    console.log("❌ MongoDB connection closed");
  }
}

