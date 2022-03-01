let _url;
if (process.env.NODE_ENV == "development") {
    //本地开发
    _url = 'http://127.0.0.1:8000/api/'; //测试地址/
} else {
    _url = 'http://django-vue3-lyadmin.lybbn.cn/api/'; //线上地址
}
export const url = _url;
export function getbaseurl() {
    return _url
}
