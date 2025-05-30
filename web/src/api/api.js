// 引入axios
import axios from 'axios'
// 请求延时（毫秒数，如果请求话费超过了'timeout'的时间，请求将被中断）
axios.defaults.timeout = 100000
import { DBToolsApi } from './dbTools';
import { ExcelApi } from './excelTools';
import { ShingiJZApi } from './shingi/jz';
import { ConfigApi } from './config';



export const apiCs = params => {
    return axios.request(
        {
            url: '/api/cs2',
            method: 'get',
            data: params
        }
    )
};

const getTemplate = params => {
    const encodedUrl = encodeURI('/static/template/template.xlsx');
    return axios.get(encodedUrl, { responseType: 'blob' });
};

export {
    getTemplate,DBToolsApi, ExcelApi,
    ShingiJZApi,
    ConfigApi
}