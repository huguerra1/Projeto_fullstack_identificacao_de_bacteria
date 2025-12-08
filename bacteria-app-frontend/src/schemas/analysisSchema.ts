import { z } from 'zod';

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

export const analysisSchema = z.object({
  sampleName: z.string().min(3, "O nome da amostra deve ter no mínimo 3 caracteres"),
  rawFile: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, "O arquivo .raw é obrigatório")
    .refine((files) => files[0]?.size <= MAX_FILE_SIZE, "O arquivo deve ser menor que 50MB"),
  hdrFile: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, "O arquivo .hdr é obrigatório")
});

// 👇 VOCÊ PRECISA ADICIONAR ESTA LINHA NO FINAL DO ARQUIVO:
export type AnalysisFormData = z.infer<typeof analysisSchema>;