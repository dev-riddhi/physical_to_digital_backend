export interface User {
name : string;
email : string;
password : string;
createdAt : Date;
token : string;
type : "user"  | "admin" ;
}


export interface RquestHistory {
userId : number;
title : string;
fileId : number[];
requestedAt : Date;
}

