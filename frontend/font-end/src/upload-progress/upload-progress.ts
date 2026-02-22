import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { UploadFeatureState } from '../state/upload.reducer';
import { Store } from '@ngrx/store';
import * as UploadActions from '../state/upload.actions';
import * as UploadSelectors from '../state/upload.selectors';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-upload-progress',
  imports: [CommonModule],
  templateUrl: './upload-progress.html',
  styleUrl: './upload-progress.scss',
})
export class UploadProgress implements OnInit {
  job$: Observable<any>;
  progress$: Observable<number>;
  step$: Observable<string>;
  results$: Observable<any>;
  error$: Observable<string | undefined>;
  jobId;
  constructor(private store: Store<{ upload: UploadFeatureState }>, private route: ActivatedRoute) {
    this.job$ = this.store.select(UploadSelectors.selectJob);
    this.progress$ = this.store.select(UploadSelectors.selectProgress);
    this.step$ = this.store.select(UploadSelectors.selectStep);
    this.results$ = this.store.select(UploadSelectors.selectResults);
    this.error$ = this.store.select(UploadSelectors.selectError);
    this.jobId = this.route.snapshot.paramMap.get('jobId');

    console.log('in upload progress ', this.job$);
  }
  ngOnInit() {
    console.log('job id ', this.jobId);
    if (this.jobId) {
      this.store.dispatch(UploadActions.pollJobStatus({ jobId: this.jobId }));
    }
  }

  // retryUpload(formData: FormData) {
  //   this.store.dispatch(UploadActions.addFiles({ files: formData }));
  // }
}
