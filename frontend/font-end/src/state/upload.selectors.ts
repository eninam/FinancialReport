import { createFeatureSelector, createSelector } from '@ngrx/store';
import { UploadFeatureState } from './upload.reducer';

// Feature selector
export const selectUploadFeature = createFeatureSelector<UploadFeatureState>('upload');

// Select Job info
export const selectJob = createSelector(selectUploadFeature, (state) => {
  console.log(' results jobs ', state.job);
  return state.job;
});
export const selectAddedFiles = createSelector(selectUploadFeature, (state) => state.selectedFiles);

// Select Status info
export const selectStatus = createSelector(selectUploadFeature, (state) => state.status);

// Select overall progress as percentage
export const selectProgress = createSelector(selectStatus, (status) => {
  console.log(' selected status ', status);
  if (!status.total_pdfs || status.total_pdfs === 0) return 0;
  return Math.round((status.pdfs_processed / status.total_pdfs) * 100);
});

// Select current step
export const selectStep = createSelector(selectStatus, (status) => status.step);

// Select results
export const selectResults = createSelector(selectStatus, (status) => {
  console.log(' results jobs ', status.result);

  return status.result;
});

// Select errors
export const selectError = createSelector(selectUploadFeature, (state) => state.error);
