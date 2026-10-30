// pm2 on the quizocracy VM: separate process, separate database (qz), separate port (8300).
module.exports = { apps: [{
  name: 'qzprod',
  cwd: '/home/ali/projects/qz',
  script: '/home/ali/projects/qz/venv/bin/uvicorn',
  args: 'app.main:app --host 127.0.0.1 --port 8300 --env-file .env --proxy-headers',
  interpreter: 'none',
  max_memory_restart: '300M',
}]};
