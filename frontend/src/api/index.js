import axios from 'axios';

export default axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://185.154.195.252:8080/api',
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`
  }
});