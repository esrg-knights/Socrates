import React from "react";
import {Checkbox} from "material-ui";
export default class DinnerRow extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      participant: props.obj.user,
      participation: props.obj,
      work_dishes: props.obj.work_dishes,
      work_cook: props.obj.work_cook,
      work_groceries: props.obj.work_groceries,
      paid: props.obj.paid
    };

    this.changeDishes = this.changeDishes.bind(this);
    this.changeCook = this.changeCook.bind(this);
    this.changeGroceries = this.changeGroceries.bind(this);
    this.changePaid = this.changePaid.bind(this);
  }

  changeDishes(e, checked) {
    this.setState({
      work_dishes: checked
    })
  }

  changeCook(e, checked) {
    this.setState({
      work_cook: checked
    });
  }

  changeGroceries(e, checked) {
    this.setState({
      work_groceries: checked
    })
  }

  changePaid(e, checked){
    this.setState({
      paid: checked
    })
  }

  render() {
    return (
      <div>
        <p>{this.state.participant.username}</p>
        <Checkbox
          label="Dishes"
          checked={this.state.work_dishes}
          onCheck={this.changeDishes}/>
        <Checkbox
          label="Cook"
          checked={this.state.work_cook}
          onCheck={this.changeCook}/>
        <Checkbox
          label="Groceries"
          checked={this.state.work_groceries}
          onCheck={this.changeGroceries}/>
        <Checkbox
          label="Paid"
          checked={this.state.paid}
          onCheck={this.changePaid} />
      </div>
    )
  }
}