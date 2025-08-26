import { Request, Response } from "express";

export function loginController(req: Request, res: Response) : Response {
    return res.json({ msg: "Login route is working!" });
}

export function signupController(req: Request, res: Response) : Response {
    return res.json({ msg: "Signup route is working!" });
}