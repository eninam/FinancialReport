import { createReducer, on } from '@ngrx/store';
import * as UploadActions from './upload.actions';
import { Job, Status, initialJob, initialStatus } from './upload.state';

export interface UploadFeatureState {
  selectedFiles: File[];
  job: Job;
  status: Status;
  error?: string;
}

export const initialUploadFeatureState: UploadFeatureState = {
  job: initialJob,
  status: initialStatus,
  error: undefined,
  selectedFiles: [],
};

export const uploadReducer = createReducer(
  initialUploadFeatureState,

  // Upload triggered: reset job and status
  on(UploadActions.addFiles, (state) => ({
    ...state,
    job: initialJob,
    status: initialStatus,
    error: undefined,
  })),

  // Backend returns Job after upload
  on(UploadActions.uploadedJob, (state, { job }) => {
    console.log('job in reducer', job);
    return {
      ...state,
      job,
      error: undefined,
    };
  }),
  on(UploadActions.selectedFiles, (state, { newSelectedFiles }) => {
    console.log('selectedFiles in reducer ', newSelectedFiles);
    return {
      ...state,
      selectedFiles: [...state.selectedFiles, ...newSelectedFiles],
    };
  }),

  // Polling returns updated status
  on(UploadActions.jobStatus, (state, { result }) => {
    console.log('result of status ', result);
    return {
      ...state,
      status: {
        ...state.status,
        ...result,
        pdfs_processed: result.pdfs_processed ?? state.status.pdfs_processed,
        total_pdfs: result.total_pdfs ?? state.status.total_pdfs,
        step: result.step ?? state.status.step,
        errors: result.errors ?? state.status.errors,
        result: result.result ?? state.status.result,
      },
    };
  }),

  // Any upload or polling error
  on(UploadActions.uploadError, (state, { error }) => ({
    ...state,
    error,
  }))
);
