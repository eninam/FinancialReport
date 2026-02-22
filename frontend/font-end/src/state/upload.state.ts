export interface Job {
  job_id: string;
  total_files: number;
  status: 'processing' | 'completed' | 'failed';
}
export interface alerts {
  category: string;
  over_by: number;
  message: string;
}
export interface savings_suggestions {
  category: string;
  action: string;
  message: string;
  amount: number;
}
export interface Status {
  pdfs_processed: number;
  total_pdfs: number;
  step: string;
  errors?: [];
  result?: {
    average_monthly_income: number;
    categories: {
      spent: number;
      percentage_of_income: number;
      delta_to_range: number;
      status: string;
      suggested_range: {
        min: number;
        max: number;
      };
    };
    alerts: alerts[];
    savings_suggestions: savings_suggestions[];
  };
}
export const initialJob: Job = {
  job_id: '',
  total_files: 0,
  status: 'processing',
};

export const initialStatus: Status = {
  pdfs_processed: 0,
  total_pdfs: 0,
  step: '',
  errors: [],
  result: {
    average_monthly_income: 0,
    categories: {
      spent: 0,
      percentage_of_income: 0,
      delta_to_range: 0,
      status: '',
      suggested_range: {
        min: 0,
        max: 100,
      },
    },
    alerts: [],
    savings_suggestions: [],
  },
};
