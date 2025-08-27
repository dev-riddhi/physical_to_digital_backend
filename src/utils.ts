import { randomBytes } from "crypto";


interface Data{
    token: string;
    type: "user" | "admin";
}

export function responseSuccess(data: Data , code : number, message : string){
    return{
        code,
        message,
        data
    };
}

export function responseError(code: number ,message : string) {
    return {
        code,
        message,
    };
}



export function generateToken(length: number = 32): string {
  return randomBytes(length).toString("hex"); // hex makes it twice the length
}