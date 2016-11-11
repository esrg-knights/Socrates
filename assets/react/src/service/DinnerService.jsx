import ApiService from "./ApiService";

export class DinnerService {
  get(page) {
    page = page ? page : '1'

    return new ApiService().get('dinner')
  }
}