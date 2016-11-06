export default class ApiService {
  post(url, data) {
    var form_data = new FormData();

    for (var key in data) {
      form_data.append(key, data[key]);
    }

    return fetch(url, {
      method: 'POST',
      body: form_data
    }).then(response => response.json())
  }
}
