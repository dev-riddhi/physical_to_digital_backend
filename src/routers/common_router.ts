import { Router } from "express";
import { loginController, signupController } from "../controllers/common_controller";

const router = Router();

// Common route
router.post("/login", loginController);
router.post("/signup", signupController);

export default router;