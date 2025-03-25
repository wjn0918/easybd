// 引入axios
import axios from 'axios'
// 请求延时（毫秒数，如果请求话费超过了'timeout'的时间，请求将被中断）
axios.defaults.timeout = 100000


export class Base{
    constructor(url){
        this.url = url
    }

    cs(file){
        console.log(file)
        return axios.request(
            {
                url: `${this.url}/upload`,
                method: 'post',
                body: file,
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        )
    }
}