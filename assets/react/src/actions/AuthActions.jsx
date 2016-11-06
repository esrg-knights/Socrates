export const LOGIN_SUCCESFULL = "LOGIN_SUCCESFULL";

export function successfullLogin(username, jwt) {
  localStorage.setItem("jwt", jwt);
  localStorage.setItem("username", username);

  return {
    type: LOGIN_SUCCESFULL,
    username,
    jwt
  };
}