import { Routes } from '@angular/router';

import { Upload } from '../upload/upload';
import { UploadProgress } from '../upload-progress/upload-progress';

export const routes: Routes = [
  { path: '', component: Upload },
  { path: 'progress/:jobId', component: UploadProgress },
];
