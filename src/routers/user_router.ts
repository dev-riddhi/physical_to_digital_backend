import { Router } from "express";
import { userAuthMiddleware } from "../middlewares/user_middleware";

const router = Router();

router.use(userAuthMiddleware);



export default router;
