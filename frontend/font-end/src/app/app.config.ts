import { ApplicationConfig, provideBrowserGlobalErrorListeners, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { uploadReducer } from '../state/upload.reducer';
import { UploadEffects } from '../state/upload.effects';
import { UploadService } from '../services/upload-service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // NgRx Store
    provideStore({
      upload: uploadReducer,
    }),

    // Effects
    provideEffects([UploadEffects]),
    provideBrowserGlobalErrorListeners(),
    UploadService,

    provideStoreDevtools({ maxAge: 25, logOnly: !isDevMode() }),
  ],
};
