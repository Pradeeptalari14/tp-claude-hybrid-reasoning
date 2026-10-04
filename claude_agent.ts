import Anthropic from '@anthropic-ai/sdk';

async function main() {
  const apiKey = process.env.ANTHROPIC_API_KEY || '';
  if (!apiKey) {
    console.log("ANTHROPIC_API_KEY not set; running validation simulation mode.");
    return;
  }

  const anthropic = new Anthropic({ apiKey });
  const stream = await anthropic.messages.create({
    model: 'claude-3-7-sonnet-20250219',
    max_tokens: 8192,
    thinking: {
      type: 'enabled',
      budget_tokens: 4096
    },
    messages: [
      { role: 'user', content: 'Design a zero-downtime distributed Redis cluster upgrade plan.' }
    ],
    stream: true,
  });

  for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta') {
      if ('thinking' in chunk.delta) {
        process.stdout.write(`\x1b[33m${chunk.delta.thinking}\x1b[0m`);
      } else if ('text' in chunk.delta) {
        process.stdout.write(chunk.delta.text || '');
      }
    }
  }
}

main().catch(console.error);
