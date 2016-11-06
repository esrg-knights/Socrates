export const LOGIN_SUCCESFULL = "LOGIN_SUCCESFULL";

export function succesfullLogin(username, jwt) {
  localStorage.setItem("jwt", jwt);
  return {
    type: LOGIN_SUCCESFULL,
    username,
    jwt
  };
}