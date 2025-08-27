import { Router } from "express";
import { userAuthMiddleware } from "../middlewares/user_middleware";

const router = Router();

router.use(userAuthMiddleware);

router.get("/gethistory", (req, res) => {
  // fetch user profile logic here
  res.status(200).json({ message: "User profile data" });
}); 
 
router.post("logout", (req, res) => {
  // logout logic here
  res.status(200).json({ message: "User logged out successfully" });
});

export default router;