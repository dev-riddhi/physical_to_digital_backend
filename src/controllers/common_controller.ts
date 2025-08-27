import { Request, Response } from "express";
import { getUserByEmail, createUser, updateUser } from "../models/user_model";
import { responseSuccess, responseError, generateToken } from "../utils";

interface LoginData {
  email: string;
  password: string;
}

interface SignupData {
  name: string;
  email: string;
  password: string;
}

enum FailureCode {
  USER_NOT_FOUND = 404,
  INVALID_CREDENTIALS = 401,
  SERVER_ERROR = 500,
  USER_ALREADY_EXISTS = 400,
}

enum SuccessCode {
  SUCCESS = 200,
  CREATED = 201,
}

export async function loginController(
  req: Request,
  res: Response
): Promise<Response> {
  let requesData: LoginData = req.body;

  let userData = await getUserByEmail(requesData.email);

  if (!userData) {
    return res
      .status(404)
      .json(responseError(FailureCode.USER_NOT_FOUND, "User not found!"));
  }

  if (userData.password !== requesData.password) {
    return res
      .status(401)
      .json(
        responseError(FailureCode.INVALID_CREDENTIALS, "Invalid credentials!")
      );
  }

  let token = generateToken(16);
  await updateUser(userData._id.toString(), { token });

  return res.json(
    responseSuccess(
      { token: userData._id.toString() , type: userData.type },
      SuccessCode.SUCCESS,
      "Login successful!"
    )
  );
}

export async function signupController(
  req: Request,
  res: Response
): Promise<Response> {
  let requesData: SignupData = req.body;

  let userData = await getUserByEmail(requesData.email);

  if (userData) {
    return res
      .status(400)
      .json(
        responseError(FailureCode.USER_ALREADY_EXISTS, "User already exists!")
      );
  }

  let token = generateToken(16);

  let userCreated = await createUser({
    name: requesData.name,
    email: requesData.email,
    password: requesData.password,
    createdAt: new Date(),
    token: token,
    type: "user",
  });

  if (!userCreated) {
    return res
      .status(500)
      .json(responseError(FailureCode.SERVER_ERROR, "Server error!"));
  }
  return res.json(
    responseSuccess(
      { token: token , type: "user"},
      SuccessCode.CREATED,
      "User created successfully!"
    )
  );
}
