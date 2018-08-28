//
//  ViewController.m
//
//  Created by Ruslan Baratov on 03/07/15.
//  Copyright (c) 2015 Ruslan Baratov. All rights reserved.
//

#import "ViewController.h"

#include <string>

#include <bar/bar.hpp>

@interface ViewController ()
@property (weak, nonatomic) IBOutlet UIButton *button;
@end

@implementation ViewController

- (IBAction)pushButton {
  NSString* url = @"https://github.com/forexample/ios-dynamic-framework";
  [[UIApplication sharedApplication] openURL:[NSURL URLWithString:url]];
}

- (void)viewDidLoad {
  [super viewDidLoad];
  // Do any additional setup after loading the view, typically from a nib.

  bar();
  NSString* nsstring = [NSString stringWithUTF8String:"Dynamic framework"];
  [_button setTitle:nsstring forState:UIControlStateNormal];
}

- (void)didReceiveMemoryWarning {
  [super didReceiveMemoryWarning];
  // Dispose of any resources that can be recreated.
}

@end
