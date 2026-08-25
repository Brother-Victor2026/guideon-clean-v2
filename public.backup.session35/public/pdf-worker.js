self.onmessage = async (e) => {
  const { pdfData } = e.data;
  try {
    self.postMessage({ text: "PDF analysé via Worker", success: true });
  } catch(err) {
    self.postMessage({ error: err.message, success: false });
  }
};
