import { Component, OnDestroy, OnInit } from '@angular/core';
import { HttpClient, HttpEventType, HttpHeaders } from '@angular/common/http';
import { Store } from '@ngrx/store';
import * as UploadActions from '../state/upload.actions';
import { CommonModule } from '@angular/common';
import * as UploadSelectors from '../state/upload.selectors';

@Component({
  selector: 'app-upload',
  imports: [[CommonModule]],
  templateUrl: './upload.html',
  styleUrl: './upload.scss',
})
export class Upload implements OnInit, OnDestroy {
  selectedFiles: File[] = [];
  uploadProgress: number = 0;
  selectAddedFiles$;

  constructor(private http: HttpClient, private store: Store<any>) {
    this.selectAddedFiles$ = this.store.select(UploadSelectors.selectAddedFiles);
  }
  ngOnDestroy(): void {}
  ngOnInit(): void {
    this.selectAddedFiles$.subscribe((files) => {
      this.selectedFiles = files;
    });
  }

  onFileSelected(event: any) {
    this.selectedFiles = Array.from(event.target.files);
    this.store.dispatch(UploadActions.selectedFiles({ newSelectedFiles: this.selectedFiles }));
  }

  uploadFiles() {
    if (this.selectedFiles.length === 0) return;
    const formData = new FormData();
    for (let file of this.selectedFiles) {
      console.log('selected file ', file);
      formData.append('files', file);
      console.log(' from data in for ', formData.get('files'));
    }
    console.log('formData formData ', formData.getAll('files'));

    this.store.dispatch(UploadActions.addFiles({ files: formData }));
  }
}
