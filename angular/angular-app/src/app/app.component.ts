import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [FormsModule, CommonModule],
  standalone: true,
})
export class AppComponent {
  startDate: string = '';
  endDate: string = '';
  currencyRates: any = {};

  constructor() {}

  submitRequest() {
    const url = `http://localhost:80/api/currency-rates/?start_date=${this.startDate}&end_date=${this.endDate}`;

    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        return response.json();
      })
      .then(data => {
        this.currencyRates = this.groupByDate(data);
      })
      .catch(error => {

      });
  }

  groupByDate(data: any[]) {
    const groupedData = data.reduce((acc, curr) => {
      const date = new Date(curr.date);
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const quarter = Math.floor((date.getMonth() + 3) / 3);
      const day = date.getDate();

      if (!acc[year]) acc[year] = {};
      if (!acc[year][`Q${quarter}`]) acc[year][`Q${quarter}`] = {};
      if (!acc[year][`Q${quarter}`][month]) acc[year][`Q${quarter}`][month] = {};
      if (!acc[year][`Q${quarter}`][month][day]) acc[year][`Q${quarter}`][month][day] = [];

      acc[year][`Q${quarter}`][month][day].push(curr);
      return acc;
    }, {});
    return groupedData;
  }

  onDateChange(event: any, isStart: boolean) {
    if (isStart) {
      this.startDate = event.target.value;
    } else {
      this.endDate = event.target.value;
    }
  }

  getKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  getMonthName(month: string): string {
    return [
      'January', 'February', 'March', 'April', 'May', 'June', 
      'July', 'August', 'September', 'October', 'November', 'December'
    ][parseInt(month)];
  }
}