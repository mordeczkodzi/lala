// ESRGAN-slim (UpscalerJS, RDN) na CPU przez tfjs wasm. stdin: surowe klatki RGB WxH, stdout: klatki RGB (W*s)x(H*s)
const tf = require('@tensorflow/tfjs');
const wasm = require('@tensorflow/tfjs-backend-wasm');
const fs = require('fs'), path = require('path');
const [,, W, H, SCALE, MODEL='slim'] = process.argv; const w=+W, h=+H, s=+SCALE;
const dir = path.join(__dirname, 'node_modules/@upscalerjs/esrgan-'+MODEL+'/models/x'+s);
const io = { load: async () => { const m = JSON.parse(fs.readFileSync(path.join(dir,'model.json')));
  const bufs = m.weightsManifest.flatMap(g => g.paths.map(p => fs.readFileSync(path.join(dir,p))));
  const total = Buffer.concat(bufs); return { modelTopology: m.modelTopology, weightSpecs: m.weightsManifest.flatMap(g=>g.weights),
  weightData: total.buffer.slice(total.byteOffset, total.byteOffset+total.byteLength) }; } };
(async () => {
  wasm.setWasmPaths(path.join(__dirname,'node_modules/@tensorflow/tfjs-backend-wasm/dist/')+'/');
  await tf.setBackend(process.env.BK || 'wasm'); await tf.ready();
  const model = await tf.loadLayersModel(io);
  const fsz = w*h*3; let buf = Buffer.alloc(0); let n=0; const t0=Date.now();
  const proc = async (frame) => {
    const out = tf.tidy(() => { const x = tf.tensor3d(new Uint8Array(frame), [h,w,3], 'int32').toFloat().expandDims(0);
      return model.predict(x).squeeze().clipByValue(0,255).round().toInt(); });
    const d = await out.data(); out.dispose(); process.stdout.write(Buffer.from(Uint8Array.from(d)));
    n++; process.stderr.write(`klatka ${n} (${((Date.now()-t0)/n/1000).toFixed(2)} s/kl)\r`);
  };
  const chunks=[]; for await (const c of process.stdin) chunks.push(c);
  const all = Buffer.concat(chunks); for (let o=0; o+fsz<=all.length; o+=fsz) await proc(all.subarray(o,o+fsz));
  process.stderr.write('\n');
})();
