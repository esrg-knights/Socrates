export default class ApiService {
  formatUrl(endpoint) {
    return API_URL + endpoint
  }

  post(endpoint, data) {
    var form_data = new FormData();

    for (var key in data) {
      form_data.append(key, data[key]);
    }

    return this.authorizedFetch(this.formatUrl(endpoint), {
      method: 'POST',
      body: form_data
    }).then(response => response.json())
  }

  get(endpoint){
    return this.authorizedFetch(this.formatUrl(endpoint), {
      method: 'GET',
    }).then(response => response.json())
  }

  authorizedFetch(url, payload){
    var myHeaders = new Headers();

    if(localStorage.getItem("jwt") != ""){
      var token = localStorage.getItem("jwt");
      console.log(token);
      myHeaders.append("Authorization", `JWT ${token}`)
    }

    payload.headers = myHeaders;

    return fetch(url, payload)
  }
}
