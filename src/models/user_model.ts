// services/userService.ts
import { ObjectId, Db } from "mongodb";
import { User } from "./schema";
import { connectDB, disconnectDB } from "../db";

const collectionName = "users";

async function getUserCollection() {
  const db: Db = await connectDB();
  return db.collection<User>(collectionName);
}

// Create
export async function createUser(user: User) {
  try {
    const users = await getUserCollection();
    user.createdAt = new Date();
    const result = await users.insertOne(user);
    return result.insertedId;
  } catch (err) {
    return false;
  }
}

// Read
export async function getUserByEmail(email: string) {
  const users = await getUserCollection();
  return users.findOne({ email: email });
}

// Update
export async function updateUser(id: string, updates: Partial<User>) {
  const users = await getUserCollection();
  await users.updateOne({ _id: new ObjectId(id) }, { $set: updates });
  return true;
}

// Delete
export async function deleteUser(id: string) {
  const users = await getUserCollection();
  await users.deleteOne({ _id: new ObjectId(id) });
  return true;
}
