import type { UserProps, ErrorProps } from "../types";
import api from "./api";

export async function getAll(): Promise<UserProps[] | ErrorProps> {
  const { data } = await api.get("/");
  return data;
}

export async function register(name:string, email:string): Promise<UserProps | ErrorProps> {
  const { data } = await api.post("/", { name, email });
  return data;
}