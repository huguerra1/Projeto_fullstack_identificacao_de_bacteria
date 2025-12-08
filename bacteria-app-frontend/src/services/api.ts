import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export interface UploadPayload {
  sampleRaw: File;
  sampleHdr: File;
  darkRaw: File;
  darkHdr: File;
  whiteRaw: File;
  whiteHdr: File;
  snv: boolean;
  savgol: boolean;
}

export const analyzeSample = async (payload: UploadPayload) => {
  const formData = new FormData();
  
  // Amostra
  formData.append('sample_raw', payload.sampleRaw);
  formData.append('sample_hdr', payload.sampleHdr);
  // Dark
  formData.append('dark_raw', payload.darkRaw);
  formData.append('dark_hdr', payload.darkHdr);
  // White
  formData.append('white_raw', payload.whiteRaw);
  formData.append('white_hdr', payload.whiteHdr);
  
  // Opções
  formData.append('snv', String(payload.snv));
  formData.append('savgol', String(payload.savgol));

  const response = await api.post('/api/analyze', formData);
  return response.data;
};