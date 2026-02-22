import { Injectable } from '@angular/core';
import { HttpClient, HttpEventType, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UploadService {
  uploadUrl = 'http://localhost:8000/upload';
  private jobUrl = 'http://localhost:8000/status'; // endpoint to poll job status

  constructor(private http: HttpClient) {}

  startUpload(files: FormData): Observable<any> {
    console.log(' stat upload ', files);
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    return this.http.post(this.uploadUrl, formData);
  }

  getJobStatus(jobId: string): Observable<any> {
    console.log(' get job status ', jobId);
    return this.http.get(`${this.jobUrl}/${jobId}`, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
      withCredentials: true,
    });
  }
}
