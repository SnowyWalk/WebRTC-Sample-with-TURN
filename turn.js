const Turn = require('node-turn');

// no-auth 모드로 3478 포트 열기
const server = new Turn({
  authMech: 'none',
  listeningPort: 3478,
  realm: 'local',
  debugLevel: 'ALL'
});

server.start();
console.log('Node-TURN 서버 실행 중 on 0.0.0.0:3478');
