class Achievement extends React.Component {

    calcBadgeWidth() {
            // set the width of the badge
            // Correct for the counter
        var badgeRatio;
        if (this.props.showCounter == 0)
            badgeRatio = 6.8 / 11.0;
        else
            badgeRatio = 5.0 / 9.0;

                //// TODO: Possible future implementation, calculation based on badge image size??

        // return the Width of the element
        var a = Math.round(this.props.height * badgeRatio);
        return a;
    }
    calcMarkerTextSize(){
        var targetSize = 1;
        var targetHeight = 200.0;

        return targetSize * (this.props.height / targetHeight) + 'em';
    }
    calcCounterTextSize(){
        var targetSize = 1.2;
        var targetHeight = 100.0;

        return targetSize * (this.props.height / targetHeight) + 'em';
    }
    calcTopMargin() {
        // If counter is present, display banner with a 10% offset

        if (this.props.showCounter == 0) {
            return 0;}
        return 10;
    }

    // Return the style of the banner
    getBannerStyle(){

        var BadgeImage = '/media/'+this.props.info.imageName;
        if (this.props.info.imageName == ""){
            BadgeImage = "/static/achievements/img/Ach_ERROR.png";
        }
        else
        {
            BadgeImage = '/media/'+this.props.info.imageName;
        }
        var bannerTopMargin, bannerHeight;


        // Create the offset for the banner if the counter is present
        bannerTopMargin = this.calcTopMargin();
        bannerHeight = 100 - bannerTopMargin;

        return {width: "100%",
                top: bannerTopMargin + '%',
                height: bannerHeight + '%',
                backgroundImage: 'url('+BadgeImage+')',
                backgroundSize: '100% 100%'
                };
    }


    clickOccured() {
        // The Achievement has been clicked, activate the associated event
        if (this.props.clickHandler != null)
            if (this.props.index > -1)
            {
                this.props.clickHandler(this.props.index);
            }
            else
                this.props.clickHandler();
    }

    constructor(props) {
        super(props);

        this.markerTitle="Obtained";
    }

    render() {
            // the Width of the intell is the width of the element - the widthe of the badge - the left padding
        var intellLeftPadding = 10;
        var achStyle = {height: this.props.height + 'px'};
        if (this.props.showIntell == 0)
            achStyle = {height: (this.props.height + 'px'), maxWidth: (this.calcBadgeWidth() + 'px')};

        var className = "Achievement "+ this.props.styleClass;
        if (this.props.styleClass == "")
            className = "Achievement";

        return (
         <div className={className} style={achStyle}>
            {this.SetUpAchievementBadge()}
            {this.SetUpAchievementIntell()}
         </div>
        );

     }
    SetUpAchievementBadge() {

                /// Check if Badge should appear clickable
             var mouseAppearance = "auto";
             if (this.props.clickHandler != null)
                mouseAppearance = "pointer";

                 /// Calculate the width of the Badge Element and set the correct style
             var styleBadge = {width: (this.calcBadgeWidth() + 'px'), cursor: mouseAppearance};
             var styleMarker, styleBanner;

             if (this.props.showCounter == 0)
             {
                 styleMarker = { display: 'none'};
                 styleBanner = { top: '0%'};
             }
             else
             {
                var markerImage; // = "../Images/Marker_empty_obtained.png";
                    /// Set the marker to the right image
                if (this.props.showIfObtained == 1)
                {
                    if (this.props.info.obtained == 1)
                        markerImage = "Marker_empty_obtained.png";
                    else
                        markerImage = "Marker_empty.png";
                        //http://i.imgur.com/UNSlAS1.png

                }
                else
                    markerImage = "Marker_empty_obtained.png";

                 styleMarker = {display: 'initial',
                                backgroundImage: 'url(/static/achievements/img/'+markerImage+')',
                                backgroundSize: '100% 100%'};
             }

             return (<div className="ach_Badge" style={styleBadge} onClick={() => this.clickOccured()}>
                         <div className="ach_banner" style={this.getBannerStyle()}></div>
                         <div className="ach_Marker" style={styleMarker}>
                             <div className="ach_markerIMG"></div>
                             <div className="ach_markerTitle" style={{fontSize: this.calcMarkerTextSize()}}>{ this.markerTitle}</div>
                             <div className="ach_markerCounter" style={{fontSize: this.calcCounterTextSize()}}>{this.props.info.count}</div>
                         </div>
                     </div>);
         }
    SetUpAchievementIntell() {
        // Create the content to form the Intell


        var styleIntell, styleIntellContent;
            // If Intell should be shown
        if (this.props.showIntell == 1)
        {
            var intellPaddingLeft = this.calcBadgeWidth();
            var intellPaddingTop = this.calcTopMargin();

                /// Set the intell to visible, set the top padding and correct the max height accordingly
            styleIntell = {display: 'initial',
                           paddingTop: intellPaddingTop + '%',
                           maxHeight: (100-intellPaddingTop) + '%'};
                /// Move all elements in the intell to make room for the badge to be visible
                /// It is done this way so the width does never exceed the Achievement width while also allowing text to be centered in the popUp window
            styleIntellContent  = {marginLeft: intellPaddingLeft + 'px'}
        }
        else    /// element should not be displayed
            styleIntell = {display: 'none'};

        var link = this.props.info.link;
        if (link == "-")
            link = "";

            /// Return the collection of Intell elements
        return (
            <div className="ach_Intell" style={styleIntell}>
               <div className="ach_intellName" style={styleIntellContent}>{this.props.info.name}</div>
               <div className="ach_intellKind" style={styleIntellContent}>{link}</div>
               <div className="ach_intellDesc" style={styleIntellContent}>{this.props.info.desc}</div>
            </div>
        )
    }
}

Achievement.defaultProps = {
  info:"",
  index: -1,
  width: "550",
  height: "200",
  showCounter: 1,
  showIfObtained: 1,
  showIntell: 1};

////////////////////////////////////////////////////////////////
////////////////ACHIEVEMENT COLLECTION OBJECT///////////////////
////////////////////////////////////////////////////////////////

/*
This object displays a range of Achievements.
It also creates the PopUp when an Achievement has been clicked.
*/
class AchievementCollection extends React.Component {

    createPopUp(index){
        var content = <div><PopUpContent_Achievement index={index} winners={this.props.achievements.winners} partOf={this.props.achievements}/></div>;
        CreatePopUpWithContent(this.props.title, content);
    }

    render(){
        var achievementObjectList = []; // The list in which all AchievementDOMs will be contained

            // Loop over and render all achievements
        var achElement;
        var achInfo;
        for (var i = 0; i < this.props.achievements.length; i++) {
                // Create the Achievement object
            achElement = (<Achievement
                            key={i}
                            index={i}
                            info={this.props.achievements[i]}
                            showIntell={this.props.showIntell}
                            showCounter={this.props.showCounter}
                            width={this.props.width}
                            styleClass={this.props.styleClass}
                            height={this.props.height}
                            clickHandler={(index) => this.createPopUp(index)}
                            />);
                // Add the Achievement React object onto the list
            achievementObjectList.push(achElement);
        }
            // Return the list of Achievement is a contained Div
        return (
            <div className="AchievementCollection">
                {achievementObjectList}
            </div>
        );
    }

}

AchievementCollection.defaultProps = {
  achievements: "",
  width: "550",
  height: "200",
  showCounter: 1,
  showIntell: 1};

////////////////////////////////////////////////////////////////
///////////////////POP UP CONTENT EXTENSION/////////////////////
///////////////////      ACHIEVEMENT       /////////////////////
////////////////////////////////////////////////////////////////

/*
This object displays contains an Achievement in a list of achievements that can be toggled through
It is ideally to be used for displaying in Pop-ups
*/
class PopUpContent_Achievement extends React.Component{

    constructor(props){
        super(props);

            // Get the starting index and store it locally
        this.index = props.index;

            // Check whether the left or right button should be visible
        var leftVisibility = 'hidden';
        var rightVisibility = 'hidden';

        if (props.index != -1)
        {
            if (props.index>0) {
                leftVisibility = 'visible';
            }
            if (props.index < props.partOf.length - 1) {
                rightVisibility = 'visible';
            }
        }

            // Set the starting states
        this.state = {achievement: props.partOf[this.index], canGoLeft: leftVisibility, canGoRight: rightVisibility};

        this.OnKeyPressed = this.OnKeyPressed.bind(this);
        document.addEventListener("keypress", this.OnKeyPressed);
    }

    componentWillUnmount() {
        document.removeEventListener("keypress", this.OnKeyPressed);
    }


    CreateObtainedNamesList(){

        // ToDo: Insert code to get all people who achieved the achievement from the server
        var nameObjects = [];
        var name;
        var title;

        for (var i = 0; i < this.props.partOf[this.index].winners.length; i++) {
                        // Create the Achievement object
                    name = (<div className="PUC_Ach_User" key={i}>{this.props.partOf[this.index].winners[i]}</div>);
                        // Add the Achievement React object onto the list
                    nameObjects.push(name);
        }

        title = "People who obtained this Achievement";
        // check whether nobody obtained it
        if (nameObjects.length == 0)
            title = "This achievement stands unclaimed"


        return (
            <div className="PUC_Ach_userBlock">
                <p className="PUC_Ach_userBlockTitle">{title}</p>
                <div className="PUC_Ach_userBlockList">
                    {nameObjects}
                </div>
            </div>);
    }

    // Change the achievement when pressing arrow keys
    OnKeyPressed(e)
    {
        // When left key is pressed
        if (e.keyCode == 37)
            this.showLeftAchievement();
        // When right key is pressed
        if (e.keyCode == 39)
            this.showRightAchievement();
    }

    showLeftAchievement()
    {
        if (this.index!=0){
            this.index--;
            var newAchievement = this.props.partOf[this.index];

            if (this.index!=0) {
                this.setState({canGoLeft:'visible', achievement: newAchievement, canGoRight:'visible'});
            }
            else {
                this.setState({canGoLeft:'hidden', achievement: newAchievement, canGoRight:'visible'});
            }
        }
    }
    showRightAchievement()
    {
        if (this.index != this.props.partOf.length - 1){
            this.index++;
            var newAchievement = this.props.partOf[this.index];

            if (this.index!= this.props.partOf.length - 1) {
                this.setState({canGoLeft:'visible', achievement: newAchievement, canGoRight:'visible'});
            }
            else{
                this.setState({canGoLeft:'visible', achievement: newAchievement, canGoRight:'hidden'});
            }
        }
    }


    render() {

        return (
            <div className="PUC_Achievement">
                <p className="PUC_Ach_Arrow" onClick={() => this.showLeftAchievement()} style={{visibility: this.state.canGoLeft}}>&#x2039;</p>
                <div className="PUC_Ach_Block">
                    <Achievement info={this.state.achievement} showIntell="1" showCounter="0" width="1500" styleClass="col-xs-12"/>
                    {this.CreateObtainedNamesList()}
                </div>
                <p className="PUC_Ach_Arrow" onClick={() => this.showRightAchievement()} style={{visibility: this.state.canGoRight}}>&#x203a;</p>
            </div>
        );
    }

}