export const LOGIN_SUCCESFULL = "LOGIN_SUCCESFULL";
export const LOGOUT = "LOGOUT";

export function successfullLogin(username, response) {
  localStorage.setItem("jwt", response.token);
  localStorage.setItem("username", username);

  return {
    type: LOGIN_SUCCESFULL,
    username,
    jwt: response.token
  };
}

export function logout(){
  localStorage.setItem("jwt", "");
  localStorage.setItem("username", "");

  return {
    type: LOGOUT,
  }
}