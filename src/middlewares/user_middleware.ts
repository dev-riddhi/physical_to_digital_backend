import { Request, Response, NextFunction } from "express";

export function userAuthMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const authHeader = req.headers.authorization;
  if (authHeader !== "simpletest") {
    return res.status(401).json({ msg: "Unauthorized" });
  }
  next();
}
