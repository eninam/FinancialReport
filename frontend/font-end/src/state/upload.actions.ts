import { createAction, props } from '@ngrx/store';
import { Job } from './upload.state';

export const addFiles = createAction('[Upload] Add Files', props<{ files: FormData }>());
export const uploadedJob = createAction('[Upload] Set Job', props<{ job: Job }>());
export const jobStatus = createAction('[Upload] Job Status', props<{ result: any }>());
export const uploadError = createAction('[Upload] Error', props<{ error: string }>());
export const pollJobStatus = createAction('[Upload] Poll Job Status', props<{ jobId: string }>());
export const selectedFiles = createAction(
  '[Upload] Save Selected files',
  props<{ newSelectedFiles: File[] }>()
);
