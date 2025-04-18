import archiver from 'archiver';
import fs from 'fs';
import path from 'path';

// 创建一个文件来写入
const output = fs.createWriteStream('ai-navigation.zip');
const archive = archiver('zip', {
  zlib: { level: 9 } // 设置压缩级别
});

output.on('close', () => {
  console.log('项目已成功导出到 ai-navigation.zip');
});

archive.on('error', (err) => {
  throw err;
});

archive.pipe(output);

// 添加文件到压缩包
archive.file('index.html', { name: 'index.html' });
archive.file('sites.csv', { name: 'sites.csv' });
archive.file('package.json', { name: 'package.json' });
archive.file('vite.config.js', { name: 'vite.config.js' });
archive.file('README.md', { name: 'README.md' });
archive.file('LICENSE', { name: 'LICENSE' });

// 完成打包
archive.finalize();