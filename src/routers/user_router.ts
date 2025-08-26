import { Router } from "express";
import { userAuthMiddleware } from "../middlewares/user_middleware";
import {loginController,signupController,} from "../controllers/user_controller";

const router = Router();

router.use(userAuthMiddleware);

router.post("/login", loginController);
router.post("/signup", signupController);

export default router;
