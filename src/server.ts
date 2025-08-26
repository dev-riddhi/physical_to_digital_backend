import express, { Request, Response } from "express";
import dotenv from "dotenv";
import userRouter from "./routers/user_router";
import adminRouter from "./routers/admin";

dotenv.config();
const app = express();
const PORT = Number(process.env.PORT) ;
const HOST = process.env.HOST ;

// middleware to parse json
app.use(express.json());


// middleware to handle user routes
app.use("/api/user", userRouter);
app.use("/api/admin", adminRouter);


// server configuration
app.listen(PORT,HOST !,() => {
  console.log(`Server running at http://localhost:${PORT}`);
});
