import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Upload } from '../upload/upload';
import { UploadProgress } from '../upload-progress/upload-progress';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Upload, UploadProgress],
  templateUrl: './app.html',
  styleUrl: './app.scss',
  standalone: true,
})
export class App {
  protected readonly title = signal('font-end');
}
