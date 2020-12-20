import { Component, OnInit,ViewChild, ElementRef } from '@angular/core';
import { RecommenderApiService } from './text-editor.service';
import {Subscription} from 'rxjs/Subscription';

@Component({
  selector: 'app-text-editor',
  templateUrl: './text-editor.component.html',
  styleUrls: ['./text-editor.component.scss'],
})
export class TextEditorComponent implements OnInit {
  config = {
    placeholder: '',
    tabsize: 2,
    height: '500px',
    uploadImagePath: '/api/upload',
    toolbar: [
        ['misc', ['codeview', 'undo', 'redo']],
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['font', ['bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript', 'clear']],
        ['fontsize', ['fontname', 'fontsize', 'color']],
        ['para', ['style', 'ul', 'ol', 'paragraph', 'height']],
        ['insert', ['table', 'picture', 'link', 'video', 'hr']]
    ],
    fontNames: ['Helvetica', 'Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Roboto', 'Times']
  }
  recommenderImagesSubscription: Subscription;
  imagesList : string[] = [];
  title : string;
  content : string;
  constructor(private recommenderApiService: RecommenderApiService) {}

  ngOnInit() {}
  suggest()
  {
    this.recommenderApiService.recommendImages(this.title + " " + this.content, 10)
      .subscribe(res => {
                  this.imagesList = res;
        },
        console.error
      );
  }
  copyLink(link: string)
  {
    var input = document.createElement('input');
    input.setAttribute('value', link);
    document.body.appendChild(input);
    input.select();
    var result = document.execCommand('copy');
    document.body.removeChild(input);
  }
}
