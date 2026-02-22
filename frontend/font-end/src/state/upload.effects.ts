import { inject, Inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import * as UploadActions from './upload.actions';
import { UploadService } from '../services/upload-service';
import { mergeMap, map, catchError, tap, switchMap, takeWhile } from 'rxjs/operators';
import { of, timer } from 'rxjs';
import { Router } from '@angular/router';

@Injectable()
export class UploadEffects {
  private actions$ = inject(Actions);
  private uploadService = inject(UploadService);
  private router = inject(Router);

  upload$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(UploadActions.addFiles),
      mergeMap((action) =>
        this.uploadService.startUpload(action.files).pipe(
          map((job) => {
            console.log('job in map', job);
            return UploadActions.uploadedJob({ job });
          }),
          catchError((err) => of(UploadActions.uploadError({ error: err.message })))
        )
      )
    );
  });

  navigateAfterUpload$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(UploadActions.uploadedJob),
        tap(({ job }) => {
          this.router.navigate(['/progress', job.job_id]);
        })
      ),
    { dispatch: false }
  );

  pollJob$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UploadActions.pollJobStatus),
      switchMap(({ jobId }) =>
        timer(0, 2000).pipe(
          // poll every 2 seconds
          switchMap(() =>
            this.uploadService
              .getJobStatus(jobId)
              .pipe(catchError((err) => of({ error: err.message })))
          ),
          takeWhile((res: any) => res?.step !== 'Analysis complete', true), // continue until step === 'analysis_complete'; true emits last value
          map((res: any) => {
            console.log('rest in poll job effect ', res);
            if (res.error) {
              return UploadActions.uploadError({ error: res.error });
            }
            return UploadActions.jobStatus({ result: res });
          })
        )
      )
    )
  );
}
