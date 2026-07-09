import { readFileSync } from 'node:fs';

const file = process.argv[2];

if (!file) {
  fail('commit-msg: 커밋 메시지 파일 경로가 없습니다.');
}

const message = readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
const lines = message.split('\n');
const title = lines[0] ?? '';
const body = lines.slice(1).join('\n').trim();
const prefixes = ['feat', 'fix', 'docs', 'chore', 'refactor', 'style', 'test'];
const titlePattern = new RegExp(`^(${prefixes.join('|')}): .+$`);
const subject = title.replace(new RegExp(`^(${prefixes.join('|')}): `), '');

if (!title.trim()) {
  fail('커밋 제목이 비어 있습니다.');
}

if (Array.from(title).length > 50) {
  fail('커밋 제목은 50자를 넘을 수 없습니다.');
}

if (!titlePattern.test(title)) {
  fail(`커밋 제목은 "{접두어}: {커밋 메시지}" 형식이어야 합니다. 접두어는 ${prefixes.join(', ')} 중 하나입니다.`);
}

if (/[.。!?！？]$/.test(subject)) {
  fail('커밋 메시지는 문장 부호 없이 명사로 끝나야 합니다.');
}

if (/(다|요|니다)$/.test(subject)) {
  fail('커밋 메시지는 서술형이 아니라 명사형으로 끝나야 합니다.');
}

if (body) {
  if ((lines[1] ?? '') !== '') {
    fail('커밋 body가 있다면 제목 다음 줄은 비워야 합니다.');
  }

  const bodyLines = body
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'));

  for (const line of bodyLines) {
    const content = line.replace(/^[-*]\s+/, '');
    if (Array.from(content).length > 72) {
      fail('커밋 body 항목은 72자 이하로 작성해야 합니다.');
    }
    if (/[.。!?！？]$/.test(content) || /(다|요|니다)$/.test(content)) {
      fail('커밋 body도 문장형 대신 명사형으로 끝나야 합니다.');
    }
  }
}

function fail(reason) {
  console.error(`commit-msg: ${reason}`);
  console.error('예: feat: 문자열 병합 기능 추가');
  process.exit(1);
}
