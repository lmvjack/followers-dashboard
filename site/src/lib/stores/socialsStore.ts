import { writable } from "svelte/store";
import type { Social } from "../interfaces/social";

export const socialsArray = writable<Social[]>([
  { name: "twitter", icon: "ph-fill ph-twitter-logo", color: "#1DA1F2" },
  { name: "instagram", icon: "ph-bold ph-instagram-logo", color: "#E1306C" },
  { name: "twitch", icon: "ph-fill ph-twitch-logo", color: "#9244ff" },
]);